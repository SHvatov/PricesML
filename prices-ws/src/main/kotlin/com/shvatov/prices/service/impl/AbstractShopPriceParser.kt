package com.shvatov.prices.service.impl

import com.shvatov.prices.data.Good
import com.shvatov.prices.service.ShopPriceParser
import org.jsoup.Jsoup
import org.jsoup.nodes.Document

/**
 * @author shvatov
 */
abstract class AbstractShopPriceParser : ShopPriceParser {
    /**
     * URL, which will be used as a template to connect
     * to the page of the web-site with the data about queried product.
     */
    protected abstract val connectionUrlTemplate: String

    override fun parseGoodsForRequestedProduct(requestedProduct: String): List<Good> {
        val document = Jsoup.connect(
            String.format(
                connectionUrlTemplate,
                requestedProduct.replace("\\s", "%20")
            )
        ).get()
        return parse(document)
    }

    /**
     * Parses the data about the products from the [document].
     */
    protected abstract fun parse(document: Document): List<Good>
}