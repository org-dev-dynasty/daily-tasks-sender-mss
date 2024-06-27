import * as cdk from 'aws-cdk-lib';
import {
    aws_cognito as cognito,
    RemovalPolicy,
    CfnOutput
} from 'aws-cdk-lib';
import {Construct} from 'constructs';

export class CognitoStack extends Construct {
    public readonly userPool: cognito.UserPool;
    public readonly client: cognito.UserPoolClient;

    constructor(scope: Construct, id: string) {
        super(scope, 'DailyTasksMssCognitoStack');

        const fromEmail = process.env.FROM_EMAIL || '';
        const replyToEmail = process.env.REPLY_TO_EMAIL || '';

        if (!fromEmail || !replyToEmail) {
            throw new Error('Missing required environment variables: SES_REGION, FROM_EMAIL, REPLY_TO_EMAIL');
        }

        const email = cognito.UserPoolEmail.withSES({
            fromEmail,
            replyTo: replyToEmail
        });

        const githubRef = process.env.GITHUB_REF || '';
        const removalPolicy = githubRef.includes('prod')
            ? RemovalPolicy.RETAIN
            : RemovalPolicy.DESTROY;

        this.userPool = new cognito.UserPool(this, 'dts_user_pool', {
            removalPolicy: removalPolicy,
            selfSignUpEnabled: true,
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

        this.client = this.userPool.addClient('dts_pool_client', {
            userPoolClientName: 'dts_pool_client',
            generateSecret: false,
            authFlows: {
                adminUserPassword: true,
                userPassword: true,
                userSrp: true
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
