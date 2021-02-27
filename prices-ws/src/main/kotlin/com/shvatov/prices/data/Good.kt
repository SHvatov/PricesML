package com.shvatov.prices.data

import com.fasterxml.jackson.annotation.JsonCreator
import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import com.fasterxml.jackson.annotation.JsonProperty
import java.math.BigDecimal

/**
 * Defines basic data representation of the record from the shop.
 * @author shvatov
 */
@JsonIgnoreProperties(ignoreUnknown = true)
data class Good @JsonCreator constructor(
    @field:JsonProperty(value = "regularPrice") val regularPrice: BigDecimal? = null,
    @field:JsonProperty(value = "discountPrice") val discountPrice: BigDecimal? = null,
    @field:JsonProperty(value = "title") val title: String? = null,
    @field:JsonProperty(value = "shop") val shop: Shop? = null,
    @field:JsonProperty(value = "pathToPicture") val pathToPicture: String? = null,
)

/**
 * Type of the shop, supported by the WS.
 */
enum class Shop(val id: Int) {
    OKEY(1),
    LENTA(2)
}