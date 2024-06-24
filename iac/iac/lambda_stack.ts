/* eslint-disable @typescript-eslint/no-explicit-any */
import { Construct } from 'constructs'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { Resource, LambdaIntegration } from 'aws-cdk-lib/aws-apigateway'
import { Duration } from 'aws-cdk-lib'
import * as path from 'path'

export class LambdaStack extends Construct {
  functionsThatNeedDynamoPermissions: lambda.Function[] = []
  lambdaLayer: lambda.LayerVersion
  sqlAlchemyLayer: lambda.LayerVersion
  PsycopgLayer: lambda.LayerVersion
  
  getAllUsersFunction: lambda.Function

  createLambdaApiGatewayIntegration(moduleName: string, method: string, mssApiResource: Resource, environmentVariables: Record<string, any>) {
    const modifiedModuleName = moduleName.toLowerCase().split(' ').map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    
    // create_user -> Create_user

    const lambdaFunction = new lambda.Function(this, modifiedModuleName, {
      functionName: `${modifiedModuleName}`,
      // need to take ../../src/modules/${moduleName} to get the correct path
      code: lambda.Code.fromAsset(path.join(__dirname, `../../src/modules/${moduleName}`)),
      handler: `app.${moduleName}_presenter.lambda_handler`,
      runtime: lambda.Runtime.PYTHON_3_11,
      layers: [this.lambdaLayer, this.sqlAlchemyLayer, this.PsycopgLayer],
      environment: environmentVariables,
      timeout: Duration.seconds(15),
      memorySize: 512
    })

    mssApiResource.addResource(moduleName.toLowerCase().replace(/_/g, '-')).addMethod(method, new LambdaIntegration(lambdaFunction))
    // /get-all-users
    return lambdaFunction
  }

  constructor(scope: Construct, apiGatewayResource: Resource, environmentVariables: Record<string, any>) {
    super(scope, 'DailyTasksMssLambdaStack')

    this.lambdaLayer = new lambda.LayerVersion(this, 'DailyTasksMssLayer', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../shared')),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
    })

    this.sqlAlchemyLayer = new lambda.LayerVersion(this, 'DailyTasksMssSqlAlchemyLayer', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../sqlalchemy')),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
    })

    this.PsycopgLayer = new lambda.LayerVersion(this, 'DailyTasksMssPsycopgLayer', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../psycopg2._psycopg')),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
    })

    
    this.getAllUsersFunction = this.createLambdaApiGatewayIntegration('get_all_users', 'GET', apiGatewayResource, environmentVariables)
  }
}