package com.shvatov.prices.service.impl

import com.shvatov.prices.GoodsCache
import com.shvatov.prices.data.Good
import com.shvatov.prices.data.GoodQuery
import com.shvatov.prices.service.ShopPriceManager
import com.shvatov.prices.service.ShopPriceParser

/**
 * @author shvatov
 */
class ShopPriceManagerImpl(
    private val queryCache: GoodsCache,
    priceParsers: List<ShopPriceParser>
) : ShopPriceManager {
    private val priceParsersByShop = priceParsers.associateBy { it.shop.id }

    override fun getGoodsForQuery(query: GoodQuery): List<Good> {
        if (query.requestedProduct == null || query.requestFrom == null) {
            return emptyList()
        }

        val keys = query.requestFrom.associatedShops.map {
            GoodsCacheKey(query.requestedProduct.hashCode(), it.id)
        }

        val cachedData = keys.associateWith { queryCache[it] }.toMutableMap()
        val missingKeys = cachedData.filter { it.value == null }.keys

        missingKeys.forEach { key ->
            val priceData = priceParsersByShop[key.shopId]
                ?.parseGoodsForRequestedProduct(query.requestedProduct)

            if (priceData != null) {
                queryCache[key] = priceData
                cachedData[key] = priceData
            }
        }

        val fetchedData = cachedData.flatMap { it.value ?: emptyList() }.sortedBy { it.discountPrice }
        return if (query.limit != null) {
            fetchedData.take(query.limit)
        } else fetchedData
    }
}

/**
 * Almost unique key for each request from the users, which consists
 * of [requestedProductHash] - hash code calculated based on [GoodQuery.requestedProduct] string
 * and id of the shop this data has been fetched from.
 */
data class GoodsCacheKey(val requestedProductHash: Int, val shopId: Int)