import { config } from 'dotenv'
import path from 'path'

config({ path: path.join(__dirname, '../.env') })

const envs = {
  STAGE: process.env.STAGE,
  STACK_NAME: process.env.STACK_NAME,
  REGION: process.env.REGION,
  AWS_ACCOUNT_ID: process.env.AWS_ACCOUNT_ID,
  SQLALCHEMY_DATABASE_URL: process.env.SQLALCHEMY_DATABASE_URL,
  MONGODB_URL: process.env.MONGODB_URL
}

export { envs }

console.log(envs)