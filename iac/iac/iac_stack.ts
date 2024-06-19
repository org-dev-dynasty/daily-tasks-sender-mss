import { Stack, StackProps } from 'aws-cdk-lib'
import { Cors, RestApi } from 'aws-cdk-lib/aws-apigateway'
import { Construct } from 'constructs'
import { LambdaStack } from './lambda_stack'
import { envs } from '../envs'

export class IacStack extends Stack {
  constructor(scope: Construct, constructId: string, props?: StackProps) {
    super(scope, constructId, props)

    const restApi = new RestApi(this, 'DailyTasksSenderMssRESTAPI', {
      restApiName: 'DailyTasksSenderMssRESTAPI',
      description: 'This is the REST API for the Daily tasks sender MSS Service.',
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        allowHeaders: ['*']
      }
    })

    const apigatewayResource = restApi.root.addResource('mss-dts', {
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        allowHeaders: Cors.DEFAULT_HEADERS
      }
    })

    // url_api_gateway/mss-dts/get-all-users

    const ENVIRONMENT_VARIABLES = {
      'STAGE': envs.STAGE
    }

    new LambdaStack(this, apigatewayResource, ENVIRONMENT_VARIABLES)

  }
}