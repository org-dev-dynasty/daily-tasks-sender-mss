import { Construct } from "constructs";
import { UserPool, UserPoolClient, UserPoolEmail } from "aws-cdk-lib/aws-cognito";
import { envs } from "../envs";

export class CognitoStack extends Construct {
  userPool: UserPool
  client: UserPoolClient
  emailSes: UserPoolEmail

  constructor(scope: Construct) {
    super(scope, `DailyTasksCognitoUserPool`)

    this.emailSes = UserPoolEmail.withSES({
      fromEmail: envs.DOMAIN_EMAIL_SES,
      
    })
    
  }
}