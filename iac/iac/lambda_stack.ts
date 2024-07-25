/* eslint-disable @typescript-eslint/no-explicit-any */
import {Construct} from 'constructs'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import {Resource, LambdaIntegration, CognitoUserPoolsAuthorizer} from 'aws-cdk-lib/aws-apigateway'
import {Duration} from 'aws-cdk-lib'
import * as path from 'path'
import { envs } from '../envs'

export class LambdaStack extends Construct {
    functionsThatNeedCognitoPermissions: lambda.Function[] = []
    lambdaLayer: lambda.LayerVersion
    libLayer: lambda.LayerVersion

    getAllUsersFunction: lambda.Function
    loginFunction: lambda.Function
    createUserFunction: lambda.Function
    confirmUserEmailFunction: lambda.Function
    createUserOAuthFunction: lambda.Function
    refreshTokenFunction: lambda.Function

    getTaskByIdFunction: lambda.Function
    createTaskFunction: lambda.Function
    getAllTasksFunction: lambda.Function
    updateTaskFunction: lambda.Function
    deleteTaskByIdFunction: lambda.Function
    getTaskByDayFunction: lambda.Function

    getAllCategoriesFunction: lambda.Function
    createCategoryFunction: lambda.Function

    createLambdaApiGatewayIntegration(
        moduleName: string, 
        method: string, 
        mssApiResource: Resource, 
        environmentVariables: Record<string, any>, 
        authorizer?: CognitoUserPoolsAuthorizer
    ): lambda.Function {
        const modifiedModuleName = moduleName.toLowerCase().split(' ').map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
        // create_user -> Create_user
        const githubRef = envs.GITHUB_REF || '';
        let stage;
        if (githubRef.includes('prod')) {
            stage = 'PROD';
        } else if (githubRef.includes('homolog')) {
            stage = 'HOMOLOG';
        } else if (githubRef.includes('dev')) {
            stage = 'DEV';
        } else {
            stage = 'TEST';
        }

        console.log(`Creating lambda function for ${modifiedModuleName} in stage ${stage}`)
        console.log(`Environment variables for ${modifiedModuleName}: ${JSON.stringify(environmentVariables)}`)
        const lambdaFunction = new lambda.Function(this, modifiedModuleName, {
            functionName: `${modifiedModuleName}-DailyTasksSenderMss-${stage}`,
            // need to take ../../src/modules/${moduleName} to get the correct path
            code: lambda.Code.fromAsset(path.join(__dirname, `../../src/modules/${moduleName}`)),
            handler: `app.${moduleName}_presenter.lambda_handler`,
            runtime: lambda.Runtime.PYTHON_3_11,
            layers: [this.lambdaLayer, this.libLayer],
            environment: environmentVariables,
            timeout: Duration.seconds(30),
            memorySize: 1024
        })

        mssApiResource.addResource(moduleName.toLowerCase().replace(/_/g, '-')).addMethod(method, new LambdaIntegration(lambdaFunction), authorizer ? {
            authorizer: authorizer
        } : undefined)
        // /get-all-users
        return lambdaFunction
    }

    constructor(
        scope: Construct, 
        apiGatewayResource: Resource, 
        environmentVariables: Record<string, any>,
        authorizer: CognitoUserPoolsAuthorizer
    ) {
        
        const githubRef = envs.GITHUB_REF || '';
        let stage;
        if (githubRef.includes('prod')) {
            stage = 'PROD';
        } else if (githubRef.includes('homolog')) {
            stage = 'HOMOLOG';
        } else if (githubRef.includes('dev')) {
            stage = 'DEV';
        } else {
            stage = 'TEST';
        }
        super(scope, `DailyTasksSenderMss-LambdaStack-${stage}`)

        this.lambdaLayer = new lambda.LayerVersion(this, `DailyTasksMssSharedLayer-${stage}`, {
            code: lambda.Code.fromAsset(path.join(__dirname, '../shared')),
            compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
        })

        this.libLayer = new lambda.LayerVersion(this, `DailyTasksMssLibLayer-${stage}`, {
            code: lambda.Code.fromAsset(path.join(__dirname, '../requirements')),
            compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
        })

        // for (const [key, value] of Object.entries(environmentVariables)) {
        //     if (key === 'USER_POOL_ID' || key === 'CLIENT_ID') {
        //         this.functionsThatNeedCognitoPermissions.push(this.getAllUsersFunction)
        //     }
        // }

        this.getAllUsersFunction = this.createLambdaApiGatewayIntegration('get_all_users', 'GET', apiGatewayResource, environmentVariables)
        this.loginFunction = this.createLambdaApiGatewayIntegration('login', 'POST', apiGatewayResource, environmentVariables)
        this.createUserFunction = this.createLambdaApiGatewayIntegration('create_user', 'POST', apiGatewayResource, environmentVariables)
        this.getTaskByIdFunction = this.createLambdaApiGatewayIntegration('get_task_by_id', 'GET', apiGatewayResource, environmentVariables, authorizer)
        this.createTaskFunction = this.createLambdaApiGatewayIntegration('create_task', 'POST', apiGatewayResource, environmentVariables, authorizer)
        this.confirmUserEmailFunction = this.createLambdaApiGatewayIntegration('confirm_user_email', 'POST', apiGatewayResource, environmentVariables)
        this.getAllTasksFunction = this.createLambdaApiGatewayIntegration('get_all_tasks', 'GET', apiGatewayResource, environmentVariables, authorizer)
        this.updateTaskFunction = this.createLambdaApiGatewayIntegration('update_task', 'PUT', apiGatewayResource, environmentVariables, authorizer)
        this.deleteTaskByIdFunction = this.createLambdaApiGatewayIntegration('delete_task_by_id', 'DELETE', apiGatewayResource, environmentVariables, authorizer)
        this.getTaskByDayFunction = this.createLambdaApiGatewayIntegration('get_task_by_day', 'GET', apiGatewayResource, environmentVariables, authorizer)
        this.createUserOAuthFunction = this.createLambdaApiGatewayIntegration('create_user_OAuth', 'POST', apiGatewayResource, environmentVariables)
        this.refreshTokenFunction = this.createLambdaApiGatewayIntegration('refresh_token', 'POST', apiGatewayResource, environmentVariables)
        this.getAllCategoriesFunction = this.createLambdaApiGatewayIntegration('get_all_categories', 'GET', apiGatewayResource, environmentVariables, authorizer)
        this.createCategoryFunction = this.createLambdaApiGatewayIntegration('create_category', 'POST', apiGatewayResource, environmentVariables, authorizer)

        this.functionsThatNeedCognitoPermissions = [
            this.loginFunction,
            this.createUserFunction,
            this.confirmUserEmailFunction,
            this.createUserOAuthFunction,
            this.refreshTokenFunction,
            this.getAllUsersFunction
        ]
    }
}