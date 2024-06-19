import { config } from 'dotenv'
import path from 'path'

config({ path: path.join(__dirname, '../.env') })

const envs = {
  STAGE: process.env.STAGE,
  STACK_NAME: process.env.STACK_NAME,
  REGION: process.env.REGION,
  AWS_ACCOUNT_ID: process.env.AWS_ACCOUNT_ID,
}

export { envs }

console.log(envs)