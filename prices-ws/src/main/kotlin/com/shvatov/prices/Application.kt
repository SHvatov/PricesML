package com.shvatov.prices

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.SerializationFeature
import com.shvatov.prices.data.Good
import com.shvatov.prices.data.GoodQuery
import com.shvatov.prices.service.ShopPriceManager
import com.shvatov.prices.service.ShopPriceParser
import com.shvatov.prices.service.impl.GoodsCacheKey
import com.shvatov.prices.service.impl.LentaPriceParser
import com.shvatov.prices.service.impl.OkeyPriceParser
import com.shvatov.prices.service.impl.ShopPriceManagerImpl
import io.ktor.application.Application
import io.ktor.application.call
import io.ktor.application.install
import io.ktor.features.CallLogging
import io.ktor.features.ContentNegotiation
import io.ktor.jackson.jackson
import io.ktor.request.path
import io.ktor.request.receive
import io.ktor.response.respond
import io.ktor.routing.post
import io.ktor.routing.routing
import io.ktor.server.engine.ShutDownUrl
import org.infinispan.Cache
import org.infinispan.configuration.cache.Configuration
import org.infinispan.configuration.cache.ConfigurationBuilder
import org.infinispan.manager.DefaultCacheManager
import org.infinispan.manager.EmbeddedCacheManager
import org.kodein.di.DI
import org.kodein.di.bind
import org.kodein.di.instance
import org.kodein.di.singleton
import org.slf4j.event.Level
import java.util.concurrent.TimeUnit

/**
 * Entry point of the application, starts the application on Netty server.
 */
fun main(args: Array<String>): Unit =
    io.ktor.server.netty.EngineMain.main(args)

typealias GoodsCache = Cache<GoodsCacheKey, List<Good>>

@Suppress("unused")
fun Application.module() {
    val di = DI {
        // mapper
        bind<ObjectMapper>() with singleton { ObjectMapper() }

        // cache
        bind<EmbeddedCacheManager>() with singleton { DefaultCacheManager() }
        bind<Configuration>() with singleton {
            ConfigurationBuilder()
                .expiration()
                .lifespan(1, TimeUnit.DAYS)
                .build()
        }
        bind<GoodsCache>() with singleton {
            instance<EmbeddedCacheManager>()
                .createCache("GOODS-CACHE", instance())
        }

        // parsers
        bind<ShopPriceParser>(tag = "lenta") with singleton { LentaPriceParser(instance()) }
        bind<ShopPriceParser>(tag = "okey") with singleton { OkeyPriceParser() }

        // manager
        bind<ShopPriceManager>() with singleton {
            ShopPriceManagerImpl(
                instance(),
                listOf(
                    instance(tag = "lenta"),
                    instance(tag = "okey")
                )
            )
        }
    }

    val productManager by di.instance<ShopPriceManager>()

    install(ContentNegotiation) {
        jackson {
            enable(SerializationFeature.INDENT_OUTPUT)
        }
    }

    install(CallLogging) {
        level = Level.INFO
        filter { call -> call.request.path().startsWith("/") }
    }

    install(ShutDownUrl.ApplicationCallFeature) {
        // The URL that will be intercepted (you can also use the application.conf's ktor.deployment.shutdown.url key)
        shutDownUrl = "/ktor/application/shutdown"

        // A function that will be executed to get the exit code of the process
        exitCodeSupplier = { 0 }
    }

    routing {
        post("/data") {
            val query = call.receive<GoodQuery>()
            val data = productManager.getGoodsForQuery(query)
            call.respond(data)
        }
    }
}

