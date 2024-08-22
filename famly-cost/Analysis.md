:money_with_wings: AWS Billing walkthrough for April, 2024 --> May, 2024 :money_with_wings:
- Overall cost decrease $91.7K -> 89.2K

Key changes by account:
    Production
    $41K -> $43K (We stopped reserving Database Instances so we now pay for them in this account. We also see an increase in general usage. More information about the Reserve Instances Strategy here:https://famlyapp.slack.com/archives/C034GNPEAFM/p1715073242095789)

    Control Tower
    $19.5K -> $18.5K(The Reserved Instances were billed in this account, so we see a gain now that we stopped reserving.)

    Qrvey
    $14K -> $10.5K(Details below, related to DynamoDB,Lambda and SQS)

    Staging
    $2K -> $2.6K(Most of that loss is related to KMS usage. Will investigate why that is.)


Key changes by service:
    RDS(database):$17.3K -> 16K (Gains due to keeping the database backups offsite. Losses because of changing how we do Reserved Instances. ALl in all a gain)
    DynamoDB: $2.7K -> $1.1K (Gains related to Qrvey and Qrvey POC account)
    Lambda: $1500 -> $750 (Gains related to Qrvey and Qrvey POC account)
    SQS: $1000 -> 600 (Gains related to Qrvey)