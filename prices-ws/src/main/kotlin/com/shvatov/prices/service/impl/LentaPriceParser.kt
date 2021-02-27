package com.shvatov.prices.service.impl

import com.fasterxml.jackson.databind.ObjectMapper
import com.shvatov.prices.data.Good
import com.shvatov.prices.data.Shop
import com.shvatov.prices.service.ShopPriceParser
import org.jsoup.nodes.Document
import java.math.BigDecimal

/**
 * @author shvatov
 */
class LentaPriceParser(private val mapper: ObjectMapper) : AbstractShopPriceParser(), ShopPriceParser {
    override val shop = Shop.LENTA

    override val connectionUrlTemplate = CONNECTION_URL_TEMPLATE

    @Suppress("unchecked_cast")
    override fun parse(document: Document): List<Good> {
        return runCatching {
            val data = document
                .select(PRODUCT_SELECT_QUERY)
                ?.attr(PRODUCT_DATA_ATTRIBUTE)
                ?.let { mapper.readValue(it, Map::class.java) } ?: return emptyList()

            val productData = data[ROOT_ATTR] as? List<Map<String, *>> ?: return emptyList()
            return productData.map { parseGood(it) }
        }.getOrDefault(emptyList())
    }

    @Suppress("unchecked_cast")
    private fun parseGood(goodData: Map<String, *>): Good {
        return Good(
            regularPrice = parsePrice(goodData[REGULAR_PRICE_ATTR] as? Map<String, *>),
            discountPrice = parsePrice(goodData[DISCOUNT_PRICE_ATTR] as? Map<String, *>),
            title = goodData[TITLE_ATTR] as? String,
            pathToPicture = goodData[IMAGE_PATH_ATTR] as? String,
            shop = Shop.LENTA
        )
    }

    private fun parsePrice(priceData: Map<String, *>?): BigDecimal {
        priceData ?: return BigDecimal.ZERO
        val priceValue = priceData[PRICE_VALUE_ATTR] as? Double ?: return BigDecimal.ZERO
        return BigDecimal.valueOf(priceValue)
    }

    private companion object {
        const val CONNECTION_URL_TEMPLATE = "https://lenta.com/search/?searchText=%s"

        const val PRODUCT_SELECT_QUERY = "div.search-results-container"

        const val PRODUCT_DATA_ATTRIBUTE = "data-search-results"

        const val ROOT_ATTR = "skus"

        const val TITLE_ATTR = "title"

        const val IMAGE_PATH_ATTR = "imageUrl"

        const val REGULAR_PRICE_ATTR = "regularPrice"

        const val DISCOUNT_PRICE_ATTR = "cardPrice"

        const val PRICE_VALUE_ATTR = "value"
    }
}