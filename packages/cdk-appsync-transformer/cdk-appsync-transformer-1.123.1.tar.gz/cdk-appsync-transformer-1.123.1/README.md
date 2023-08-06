# AppSync Transformer Construct for AWS CDK

![build](https://github.com/kcwinner/cdk-appsync-transformer/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/kcwinner/cdk-appsync-transformer/branch/main/graph/badge.svg)](https://codecov.io/gh/kcwinner/cdk-appsync-transformer)
[![dependencies Status](https://david-dm.org/kcwinner/cdk-appsync-transformer/status.svg)](https://david-dm.org/kcwinner/cdk-appsync-transformer)
[![npm](https://img.shields.io/npm/dt/cdk-appsync-transformer)](https://www.npmjs.com/package/cdk-appsync-transformer)

[![npm version](https://badge.fury.io/js/cdk-appsync-transformer.svg)](https://badge.fury.io/js/cdk-appsync-transformer)
[![PyPI version](https://badge.fury.io/py/cdk-appsync-transformer.svg)](https://badge.fury.io/py/cdk-appsync-transformer)

## Notice

For CDK versions < 1.64.0 please use [aws-cdk-appsync-transformer](https://github.com/kcwinner/aws-cdk-appsync-transformer).

## Why This Package

In April 2020 I wrote a [blog post](https://www.trek10.com/blog/appsync-with-the-aws-cloud-development-kit) on using the AWS Cloud Development Kit with AppSync. I wrote my own transformer in order to emulate AWS Amplify's method of using GraphQL directives in order to template a lot of the Schema Definition Language.

This package is my attempt to convert all of that effort into a separate construct in order to clean up the process.

## How Do I Use It

### Example Usage

API With Default Values

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_appsync_transformer import AppSyncTransformer
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql"
)
```

schema.graphql

```graphql
type Customer
  @model
  @auth(
    rules: [
      { allow: groups, groups: ["Admins"] }
      { allow: private, provider: iam, operations: [read, update] }
    ]
  ) {
  id: ID!
  firstName: String!
  lastName: String!
  active: Boolean!
  address: String!
}

type Product
  @model
  @auth(
    rules: [
      { allow: groups, groups: ["Admins"] }
      { allow: public, provider: iam, operations: [read] }
    ]
  ) {
  id: ID!
  name: String!
  description: String!
  price: String!
  active: Boolean!
  added: AWSDateTime!
  orders: [Order] @connection
}

type Order @model @key(fields: ["id", "productID"]) {
  id: ID!
  productID: ID!
  total: String!
  ordered: AWSDateTime!
}
```

### [Supported Amplify Directives](https://docs.amplify.aws/cli/graphql-transformer/directives)

Tested:

* [@model](https://docs.amplify.aws/cli/graphql-transformer/directives#model)
* [@auth](https://docs.amplify.aws/cli/graphql-transformer/directives#auth)
* [@connection](https://docs.amplify.aws/cli/graphql-transformer/directives#connection)
* [@key](https://docs.amplify.aws/cli/graphql-transformer/directives#key)
* [@function](https://docs.amplify.aws/cli/graphql-transformer/directives#function)

  * These work differently here than they do in Amplify - see [Functions](#functions) below

Experimental:

* [@versioned](https://docs.amplify.aws/cli/graphql-transformer/directives#versioned)
* [@http](https://docs.amplify.aws/cli/graphql-transformer/directives#http)
* [@ttl](https://github.com/flogy/graphql-ttl-transformer)

  * Community directive transformer

Not Yet Supported:

* [@searchable](https://docs.amplify.aws/cli/graphql-transformer/directives#searchable)
* [@predictions](https://docs.amplify.aws/cli/graphql-transformer/directives#predictions)

### Custom Transformers & Directives

*This is an advanced feature*

It is possible to add pre/post custom transformers that extend the Amplify ITransformer. To see a simple example please look at [mapped-transformer.ts](./test/mappedTransformer/mapped-transformer.ts) in the tests section.

This allows you to modify the data either before or after the [cdk-transformer](./src/transformer/cdk-transformer.ts) is run.

*Limitation:* Due to some limitations with `jsii` we are unable to export the ITransformer interface from `graphql-transformer-core` to ensure complete type safety. Instead, there is a validation method that will check for `name`, `directive` and `typeDefinitions` members in the transformers that are passed in.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..customTransformers import PreTransformer, PostTransformer
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql",
    pre_cdk_transformers=[PreTransformer()],
    post_cdk_transformers=[PostTransformer()]
)
```

### Authentication

User Pool Authentication

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user_pool = UserPool(self, "my-cool-user-pool", ...
)
user_pool_client = UserPoolClient(self, f"{id}-client",
    user_pool=self.user_pool, ...
)
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql",
    authorization_config={
        "default_authorization": {
            "authorization_type": AuthorizationType.USER_POOL,
            "user_pool_config": {
                "user_pool": user_pool,
                "app_id_client_regex": user_pool_client.user_pool_client_id,
                "default_action": UserPoolDefaultAction.ALLOW
            }
        }
    }
)
```

#### IAM

##### Unauth Role

You can grant access to the `public` policies generated from the `@auth` transformer by using `appsyncTransformer.grantPublic(...)`. In the example below you can see we give public iam read access for the Product type. This will generate permissions for `listProducts`, `getProduct` and `Product` (to get all the fields). We then attach it to our `publicRole` using the grantPublic method.

Example:

```graphql
type Product
    @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: public, provider: iam, operations: [read] }
    ])
    @key(name: "productsByName", fields: ["name", "added"], queryField: "productsByName") {
        id: ID!
        name: String!
        description: String!
        price: String!
        active: Boolean!
        added: AWSDateTime!
        orders: [Order] @connection
}
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
identity_pool = CfnIdentityPool(stack, "test-identity-pool",
    identity_pool_name="test-identity-pool",
    cognito_identity_providers=[{
        "client_id": user_pool_client.user_pool_client_id,
        "provider_name": f"cognito-idp.{stack.region}.amazonaws.com/{userPool.userPoolId}"
    }
    ],
    allow_unauthenticated_identities=True
)

public_role = Role(stack, "public-role",
    assumed_by=WebIdentityPrincipal("cognito-identity.amazonaws.com").with_conditions(
        StringEquals={"cognito-identity.amazonaws.com:aud": f"{identityPool.ref}"},
        ForAnyValue:StringLike={"cognito-identity.amazonaws.com:amr": "unauthenticated"}
    )
)

app_sync_transformer.grant_public(public_role)
```

##### Auth Role

You can grant access to the `private` policies generated from the `@auth` transformer by using `appsyncTransformer.grantPrivate(...)`. In the example below you can see we give private iam read and update access for the Customer type. This will generate permissions for `listCustomers`, `getCustomer`, `updateCustomer` and `Customer` (to get all the fields). We then attach it to our `privateFunction` using the grantPrivate method. *You could also use an identity pool as in the unauth example above, I just wanted to show a varied range of use*

```graphql
type Customer
    @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: private, provider: iam, operations: [read, update] }
    ]) {
        id: ID!
        firstName: String!
        lastName: String!
        active: Boolean!
        address: String!
}
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
private_function = Function(stack, "test-function",
    runtime=Runtime.NODEJS_12_X,
    code=Code.from_inline("export function handler() { }"),
    handler="handler"
)

app_sync_transformer.grant_private(private_function)
```

### Functions

#### Directive Example

```graphql
type Query {
  listUsers: UserConnection @function(name: "myFunction")
  getUser(id: ID!): User @function(name: "myFunction")
}
```

There are two ways to add functions as data sources (and their resolvers)

#### Construct Convenience Method

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_function = Function(...)

# first argument is the name in the @function directive
appsync_transformer.add_lambda_data_source_and_resolvers("myFunction", "unique-id", my_function,
    name="lambdaDatasourceName"
)
```

`addLambdaDataSourceAndResolvers` does the same thing as the manual version below. However, if you want to customize mapping templates you will have to bypass this and set up the data source and resolvers yourself

#### Manually

Fields with the `@function` directive will be accessible via `appsyncTransformer.functionResolvers`. It will return a map like so:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
    "user-function"[{"type_name": "Query", "field_name": "listUsers"}, {"type_name": "Query", "field_name": "getUser"}, {"type_name": "Mutation", "field_name": "createUser"}, {"type_name": "Mutation", "field_name": "updateUser"}
    ]
```

You can grab your function resolvers via the map and assign them your own function(s). Example might be something like:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user_function = Function(...)
user_function_data_source = appsync_transformer.appsync_aPI.add_lambda_data_source("some-id", user_function)

data_source_map = {
    "user-function": user_function_data_source
}

for [function_name, resolver] in Object.entries(appsync_transformer.function_resolvers):
    data_source = dataSourceMap[functionName]
    Resolver(self.nested_appsync_stack, f"{resolver.typeName}-{resolver.fieldName}-resolver",
        api=appsync_transformer.appsync_aPI,
        type_name=resolver.type_name,
        field_name=resolver.field_name,
        data_source=data_source,
        request_mapping_template=resolver.default_request_mapping_template,
        response_mapping_template=resolver.default_response_mapping_template
    )
```

### Table Name Map

Often you will need to access your table names in a lambda function or elsewhere. The cdk-appsync-transformer will return these values as a map of table names to cdk tokens. These tokens will be resolved at deploy time. They can be accessed via `appSyncTransformer.tableNameMap`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CustomerTable: '${Token[TOKEN.1300]}',
      ProductTable"${Token[TOKEN.1346]}" , OrderTable"${Token[TOKEN.1392]}" , BlogTable"${Token[TOKEN.1442]}" , PostTable"${Token[TOKEN.1492]}" , CommentTable"${Token[TOKEN.1546]}" , UserTable"${Token[TOKEN.1596]}"
```

### Table Map

You may need to access your dynamo table L2 constructs. These can be accessed via `appSyncTransformer.tableMap`.

### Custom Table Names

If you do not like autogenerated names for your Dynamo tables you can pass in props to specify them. Use the `tableKey` value derived from the `@model` directive. Example, if you have `type Foo @model` you would use `FooTable` as the key value.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app_sync_transformer = AppSyncTransformer(stack, "test-transformer",
    schema_path=test_schema_path,
    table_names={
        "CustomerTable": customer_table_name,
        "OrderTable": order_table_name
    }
)
```

### DynamoDB Streams

There are two ways to enable DynamoDB streams for a table. The first version is probably most preferred. You pass in the `@model` type name and the StreamViewType as properties when creating the AppSyncTransformer. This will also allow you to access the `tableStreamArn` property of the L2 table construct from the `tableMap`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app_sync_transformer = AppSyncTransformer(stack, "test-transformer",
    schema_path=test_schema_path,
    dynamo_db_stream_config={
        "Order": StreamViewType.NEW_IMAGE,
        "Blog": StreamViewType.NEW_AND_OLD_IMAGES
    }
)

order_table = app_sync_transformer.table_map.OrderTable
```

A convenience method is also available. It returns the stream arn because the L2 Table construct does not seem to update with the value since we are updating the underlying CfnTable. Normally a Table construct must pass in the stream specification as a prop

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stream_arn = app_sync_transformer.add_dynamo_dBStream(
    model_type_name="Order",
    stream_view_type=StreamViewType.NEW_IMAGE
)
```

### DataStore Support

1. Pass `syncEnabled: true` to the `AppSyncTransformerProps`
2. Generate necessary exports (see [Code Generation](#code-generation) below)

### Cfn Outputs

* `appsyncGraphQLEndpointOutput` - the appsync graphql endpoint

### Code Generation

I've written some helpers to generate code similarly to how AWS Amplify generates statements and types. You can find the code [here](https://github.com/kcwinner/advocacy/tree/master/cdk-amplify-appsync-helpers).

## Versioning

I will *attempt* to align the major and minor version of this package with [AWS CDK], but always check the release descriptions for compatibility.

I currently support [![GitHub package.json dependency version (prod)](https://img.shields.io/github/package-json/dependency-version/kcwinner/cdk-appsync-transformer/@aws-cdk/core)](https://github.com/aws/aws-cdk)

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details

## License

Distributed under [Apache License, Version 2.0](LICENSE)

## References

* [aws cdk](https://aws.amazon.com/cdk)
* [amplify-cli](https://github.com/aws-amplify/amplify-cli)
* [Amplify Directives](https://docs.amplify.aws/cli/graphql-transformer/directives)
