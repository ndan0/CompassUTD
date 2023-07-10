@REM Deploying to Cloud Run
@pushd ..
@rd /S /Q "%CD%\fast_api_app\CompassUTD" & xcopy "%CD%\CompassUTD" "%CD%\fast_api_app\CompassUTD" /E /I /H /Y
@popd
@docker build -t compassutd:latest .
@docker run -p 8080:8080 compassutd:latest
@rd /S /Q "%CD%\fast_api_app\CompassUTD"
@echo Done!