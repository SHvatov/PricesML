package com.shvatov.prices.service

import com.shvatov.prices.data.Good
import com.shvatov.prices.data.GoodQuery

/**
 *
 */
interface ShopPriceManager {
    /**
     * Returns a list of [Good] found by [query].
     * First fetches data from cache, if none present - then goes to the site.
     */
    fun getGoodsForQuery(query: GoodQuery): List<Good>
}