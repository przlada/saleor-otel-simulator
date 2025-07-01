CHECKOUT_CREATE = """
mutation checkoutCreate($channel: String, $variantID: ID!, $quantity: Int!, $address: AddressInput) {
  checkoutCreate(
    input: {channel: $channel, lines: [{variantId: $variantID, quantity: $quantity}], shippingAddress: $address, billingAddress: $address}
  ) {
    checkout {
      id
      subtotalPrice {
        currency
        gross {
          amount
        }
        net {
          amount
        }
      }
      shippingMethods {
        id
        name
      }
    }
    errors {
      field
      message
    }
  }
}
"""

CATEGORY_DETAILS = """
fragment BasicProductFields on Product {
  id
  name
  thumbnail {
    url
    alt
    __typename
  }
  thumbnail2x: thumbnail(size: 510) {
    url
    __typename
  }
  __typename
}
fragment Price on TaxedMoney {
  gross {
    amount
    currency
    __typename
  }
  net {
    amount
    currency
    __typename
  }
  __typename
}
fragment ProductPricingField on Product {
  pricing {
    onSale
    priceRangeUndiscounted {
      start {
        ...Price
        __typename
      }
      stop {
        ...Price
        __typename
      }
      __typename
    }
    priceRange {
      start {
        ...Price
        __typename
      }
      stop {
        ...Price
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}
query CategoryProducts(
  $id: ID!
  $channel: String
  $attributes: [AttributeInput!]
  $after: String
  $pageSize: Int
  $sortBy: ProductOrder
  $priceLte: Float
  $priceGte: Float
) {
  products(
    after: $after
    first: $pageSize
    sortBy: $sortBy
    filter: {
      attributes: $attributes
      categories: [$id]
      minimalPrice: { gte: $priceGte, lte: $priceLte }
    }
    channel: $channel
  ) {
    totalCount
    edges {
      node {
        ...BasicProductFields
        ...ProductPricingField
        category {
          id
          name
          __typename
        }
        __typename
      }
      __typename
    }
    pageInfo {
      endCursor
      hasNextPage
      hasPreviousPage
      startCursor
      __typename
    }
    __typename
  }
}
"""


USER_DETAILS = """
fragment Address on Address {
  id
  firstName
  lastName
  companyName
  streetAddress1
  streetAddress2
  city
  postalCode
  country {
    code
    country
    __typename
  }
  countryArea
  phone
  isDefaultBillingAddress
  isDefaultShippingAddress
  __typename
}
fragment User on User {
  id
  email
  firstName
  lastName
  isStaff
  defaultShippingAddress {
    ...Address
    __typename
  }
  defaultBillingAddress {
    ...Address
    __typename
  }
  addresses {
    ...Address
    __typename
  }
  __typename
}
query UserDetails {
  me {
    ...User
    __typename
  }
}
"""
