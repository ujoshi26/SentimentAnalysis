# Modeling hybrid cloud based flow from ingestion to storage
1. Creates Azure storage automatically using terraform
2. Connects with Weather Portal using private key - You may need to change this based on your own
3. Extract the Weather based on the geo-coordinate
4. Saves the results in to a log file
5. Uploads the log into Azure Blob storage created in step 1
