import {config} from 'dotenv'
import path from 'path'

config({path: path.join(__dirname, '../.env')})

const envs = {
    STAGE: process.env.STAGE,
    STACK_NAME: process.env.STACK_NAME,
    REGION: process.env.REGION,
    AWS_ACCOUNT_ID: process.env.AWS_ACCOUNT_ID,
    MONGODB_URL: process.env.MONGODB_URL,
    FROM_EMAIL: process.env.FROM_EMAIL,
    REPLY_TO_EMAIL: process.env.REPLY_TO_EMAIL

}

export {envs}

console.log(envs)