@REM Deploying to Cloud Run
@pushd ..
@rd /S /Q "%CD%\fast_api_app\CompassUTD" & xcopy "%CD%\CompassUTD" "%CD%\fast_api_app\CompassUTD" /E /I /H /Y
@popd
@docker build -t compassutd:latest .
@docker run -d --name CompassUTD_Container -p 80:80 compassutd
@rd /S /Q "%CD%\fast_api_app\CompassUTD"
@echo Done!