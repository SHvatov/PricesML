package com.shvatov.prices.service

import com.shvatov.prices.data.Good
import com.shvatov.prices.data.Shop

/**
 * @author shvatov
 */
interface ShopPriceParser {
    /**
     * Shop this parser is used to fetch data from.
     */
    val shop: Shop

    /**
     * Parses the data from the site according to the provided [requestedProduct].
     * Returns a list of [Good] objects.
     */
    fun parseGoodsForRequestedProduct(requestedProduct: String): List<Good>
}