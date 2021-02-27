package com.shvatov.prices.service.impl

import com.shvatov.prices.data.Good
import com.shvatov.prices.data.Shop
import com.shvatov.prices.service.ShopPriceParser
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import java.math.BigDecimal

/**
 * @author shvatov
 */
class OkeyPriceParser : AbstractShopPriceParser(), ShopPriceParser {
    override val shop = Shop.OKEY

    override val connectionUrlTemplate = CONNECTION_URL_TEMPLATE

    override fun parse(document: Document): List<Good> {
        return runCatching {
            val productData = document.select(PRODUCT_SELECT_QUERY) ?: return emptyList()
            return productData.map { parseGood(it) }
        }.getOrDefault(emptyList())
    }

    private fun parseGood(element: Element?): Good {
        val title = element
            ?.select("div.product-name")
            ?.select("a")
            ?.attr("title")

        val pathToImage = element
            ?.select("div.product-image")
            ?.select("img")
            ?.attr("data-src")

        val priceElements = element?.select("div.product-price")
        val (regular, discounted) = priceElements?.let {
            val discountedPrice = it.select("span.price.label.label-red")
            val oldPrice = it.select("span.label.small.crossed")
            if (!discountedPrice.isNullOrEmpty() && !oldPrice.isNullOrEmpty()) {
                convertToDecimalPrice(discountedPrice[0].text()) to
                    convertToDecimalPrice(oldPrice[0].text())
            } else {
                val regularPrice = it.select("span.price.label")
                val decimalRegularPrice = convertToDecimalPrice(regularPrice[0].text())
                decimalRegularPrice to decimalRegularPrice
            }
        } ?: BigDecimal.ZERO to BigDecimal.ZERO

        return Good(regular, discounted, title, Shop.OKEY, pathToImage)
    }

    private fun convertToDecimalPrice(price: String): BigDecimal {
        return BigDecimal(
            price.replace(CURRENCY_SIGN, "")
                .replace(",", ".")
                .trim()
        )
    }

    private companion object {
        const val CONNECTION_URL_TEMPLATE = "https://www.okeydostavka.ru/spb" +
            "/webapp/wcs/stores/servlet/SearchDisplay?categoryId=&storeId=10653&catalogId=12052" +
            "&langId=-20&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true" +
            "&searchSource=Q&pageView=&beginIndex=0&pageSize=72&searchTerm=%s" +
            "#facet:&productBeginIndex:0&orderBy:3&pageView:&minPrice:&maxPrice:&pageSize:72&"

        const val PRODUCT_SELECT_QUERY = "div.product.ok-theme"

        const val CURRENCY_SIGN = "₽"
    }
}