package com.shvatov.prices.data

import com.fasterxml.jackson.annotation.JsonCreator
import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import com.fasterxml.jackson.annotation.JsonProperty

/**
 * Basic query to be processed by this WS.
 * @author shvatov
 */
@JsonIgnoreProperties(ignoreUnknown = true)
data class GoodQuery @JsonCreator constructor(
    @field:JsonProperty(value = "requestedProduct") val requestedProduct: String? = null,
    @field:JsonProperty(value = "requestFrom") val requestFrom: RequestFromShop? = null,
    @field:JsonProperty(value = "limit") val limit: Int? = null,
)

/**
 * Defines from which shop data must be queried.
 */
enum class RequestFromShop(val associatedShops: List<Shop>) {
    OKEY(associatedShops = listOf(Shop.OKEY)),
    LENTA(associatedShops = listOf(Shop.LENTA)),
    ALL(associatedShops = listOf(Shop.OKEY, Shop.LENTA))
}