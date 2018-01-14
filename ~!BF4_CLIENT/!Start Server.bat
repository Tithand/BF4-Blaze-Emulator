set INSTANCEDIRECTORY="%~dp0Instance"

set IP=127.0.0.1
set GAMEPORT=25200
set REMOTEADMINPORT=127.0.0.1:47200

set PINGSITE=ams
set REGION=EU
set COUNTRY=DE

cd "%~dp0"

cls && bf4_Server_Final.exe -blazeIP %IP% -patchSSL -serverInstancePath %INSTANCEDIRECTORY% -RemoteAdminPort %REMOTEADMINPORT% -GamePort %GAMEPORT% -Country %COUNTRY% -PingSite %PINGSITE% -Region %REGION%