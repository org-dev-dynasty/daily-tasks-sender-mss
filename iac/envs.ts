import {config} from 'dotenv'
import path from 'path'

config({path: path.join(__dirname, '../.env')})

const envs = {
  STACK_NAME: process.env.STACK_NAME,
  REGION: process.env.REGION,
  AWS_ACCOUNT_ID: process.env.AWS_ACCOUNT_ID,
  MONGODB_URL: process.env.MONGODB_URL,
  FROM_EMAIL: process.env.FROM_EMAIL,
  REPLY_TO_EMAIL: process.env.REPLY_TO_EMAIL,
  GOOGLE_WEB_CLIENT_ID: process.env.GOOGLE_WEB_CLIENT_ID,
  REDIRECT_URLS: process.env.REDIRECT_URLS,
  GITHUB_REF: process.env.GITHUB_REF_NAME,
  BASE_PWD_COGNITO: process.env.BASE_PWD_COGNITO,
  MAILERSEND_API_KEY: process.env.MAILERSEND_API_KEY,
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  OPENAI_MODEL: process.env.OPENAI_MODEL,
  PROMPT: process.env.PROMPT
}

export {envs}

console.log(envs)