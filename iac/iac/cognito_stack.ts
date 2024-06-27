import * as cdk from 'aws-cdk-lib';
import {
    aws_cognito as cognito,
    RemovalPolicy,
    CfnOutput
} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {envs} from "../envs";
import { AccountRecovery, CfnIdentityPool, ProviderAttribute, UserPoolDomain, UserPoolIdentityProviderGoogle } from 'aws-cdk-lib/aws-cognito';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';

export class CognitoStack extends Construct {
    public readonly userPool: cognito.UserPool;
    public readonly client: cognito.UserPoolClient;

    constructor(scope: Construct, id: string) {
      const githubRef = process.env.GITHUB_REF || '';
      
      super(scope, `${envs.STACK_NAME}CognitoStack-${githubRef}`);

      const fromEmail = envs.FROM_EMAIL || '';
      const replyToEmail = envs.REPLY_TO_EMAIL || '';
      const googleClientId = envs.GOOGLE_WEB_CLIENT_ID || '';
      const googleSecretValue = Secret.fromSecretNameV2(this, 
        `${envs.STACK_NAME}-GoogleClientSecretValue`, 
        'GOOGLE_WEB_SECRET_VALUE'
      )
      const redirectUrls = envs.REDIRECT_URLS || '';

      if (!fromEmail || !replyToEmail) {
          throw new Error('Missing required environment variables: FROM_EMAIL, REPLY_TO_EMAIL');
      }

      const email = cognito.UserPoolEmail.withSES({
          fromEmail,
          replyTo: replyToEmail
      });

      const removalPolicy = githubRef.includes('prod')
          ? RemovalPolicy.RETAIN
          : RemovalPolicy.DESTROY;

      this.userPool = new cognito.UserPool(this, 'dts_user_pool', {
          removalPolicy: removalPolicy,
          selfSignUpEnabled: true,
          accountRecovery: AccountRecovery.EMAIL_ONLY,
          userVerification: {
              emailSubject: 'Verifique seu email para acessar o Daily Tasks',
              emailBody: 'Olá, obrigado por criar sua conta no Daily Tasks! Seu código de confirmação é {####}',
              emailStyle: cognito.VerificationEmailStyle.CODE
          },
          standardAttributes: {
              email: {
                  required: true,
                  mutable: true
              },
          },
          customAttributes: {
              name: new cognito.StringAttribute({minLen: 1, maxLen: 2048, mutable: true}),
              phone: new cognito.StringAttribute({minLen: 1, maxLen: 2048, mutable: true}),
              emailVerified: new cognito.BooleanAttribute({mutable: true}),
              acceptedTerms: new cognito.BooleanAttribute({mutable: true}),
          },
          email: email
      });

      
      const googleProvider = new UserPoolIdentityProviderGoogle(this, `${envs.STACK_NAME}-GoogleProvider` , {
        clientId: googleClientId,
        clientSecretValue: googleSecretValue.secretValue,
        scopes: ['openid', 'profile', 'email'],
        attributeMapping: {
          email: ProviderAttribute.GOOGLE_EMAIL,
          givenName: ProviderAttribute.GOOGLE_GIVEN_NAME,
          familyName: ProviderAttribute.GOOGLE_FAMILY_NAME,
          phoneNumber: ProviderAttribute.GOOGLE_PHONE_NUMBERS
        },
        userPool: this.userPool
        });
          
      this.userPool.registerIdentityProvider(googleProvider)
        
      this.client = this.userPool.addClient('dts_pool_client', {
          userPoolClientName: 'dts_pool_client',
          generateSecret: false,
          authFlows: {
              adminUserPassword: true,
              userPassword: true,
              userSrp: true
          },
          oAuth: {
            flows: {
              authorizationCodeGrant: true
            },
            callbackUrls: [redirectUrls],
            logoutUrls: [redirectUrls]
          }
      });
          
      new CfnOutput(this, 'CognitoRemovalPolicy', {
        value: removalPolicy.toString(),
        exportName: 'CognitoRemovalPolicyValue'
      });
      
      new CfnOutput(this, 'UserPoolIdOutput', {
        value: this.userPool.userPoolId,
        exportName: 'UserPoolId'
      });

      new CfnOutput(this, 'ClientIdOutput', {
        value: this.client.userPoolClientId,
        exportName: 'ClientId'
      });
    }
}
