# migrate-users
Migrates users to Alma from a csv file. 

#### Pre-requisite setup
Ensure that all user groups listed in your user csv file exist in Alma.  

#### config.txt
```
[Params]
apikey: apikey 
baseurl: https://api-na.hosted.exlibrisgroup.com/almaws/v1
```

#### migrate_users.py

Takes as arguments:
- the configuration file {config.txt} as listed above
- a csv file of user records {users.csv} from the source system.  The expected fields are:
```
record_type,primary_id,first_name,last_name,user_group,email_address,email_type
```

Run as
`
python ./migrate_users.py config.txt users.csv
`
