import * as cdk from "aws-cdk-lib";
import { Stack, StackProps, aws_iam as iam, CfnOutput } from "aws-cdk-lib";
import { Cors, RestApi } from "aws-cdk-lib/aws-apigateway";
import { Construct } from "constructs";
import { LambdaStack } from "./lambda_stack";
import { CognitoStack } from "./cognito_stack";
import { envs } from "../envs";

export class IacStack extends Stack {
  constructor(scope: Construct, constructId: string, props?: StackProps) {
    super(scope, constructId, props);

    const githubRef = envs.GITHUB_REF || "";
    let stage;
    if (githubRef.includes("prod")) {
      console.log("INCLUDE CARALHO PROD");
      stage = "PROD";
    } else if (githubRef.includes("homolog")) {
      console.log("INCLUDE CARALHO HOMOSSEX");
      stage = "HOMOLOG";
    } else if (githubRef.includes("dev")) {
      console.log("INCLUDE CARALHO DEV");
      stage = "DEV";
    } else {
      console.log("INCLUDE CARALHO TESTE!");
      stage = "TEST";
    }

    const restApi = new RestApi(this, `DailyTasksSenderMssRestAPI-${stage}`, {
      restApiName: `DailyTasksSenderMssRestAPI-${stage}`,
      description:
        "This is the REST API for the Daily tasks sender MSS Service.",
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
        allowHeaders: ["*"],
      },
    });

    const apigatewayResource = restApi.root.addResource("mss-dts", {
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
        allowHeaders: Cors.DEFAULT_HEADERS,
      },
    });

    const cognitoStack = new CognitoStack(
      this,
      `DailyTasksSenderMssCognitoStack-${stage}`
    );

    const ENVIRONMENT_VARIABLES = {
      STAGE: stage,
      MONGODB_URL: envs.MONGODB_URL,
      USER_POOL_ID: cognitoStack.userPool.userPoolId,
      CLIENT_ID: cognitoStack.client.userPoolClientId,
      REGION: this.region,
    };

    const lambdaStack = new LambdaStack(
      this,
      apigatewayResource,
      ENVIRONMENT_VARIABLES
    );

    const cognitoAdminPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: ["cognito-idp:*"],
      resources: [cognitoStack.userPool.userPoolArn],
    });

    for (const fn of lambdaStack.functionsThatNeedCognitoPermissions) {
      fn.addToRolePolicy(cognitoAdminPolicy);
    }

    new CfnOutput(this, `DailyTasksSenderMssRESTAPI-${stage}`, {
      value: `${restApi.url}/mss-dts`,
      exportName: `DailyTasksSenderMssRestAPI-${stage}`,
    });
  }
}
