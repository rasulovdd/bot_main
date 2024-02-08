""" Конфигурации """
from dotenv import load_dotenv
from os import getenv
import os
from aiogram.bot.api import TelegramAPIServer

class DotEnvVariableNotFound(Exception):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __str__(self):
        return f"Variable {self.variable_name} not found in .env file"

class Configuration:
    def __init__(self):
        load_dotenv()
        self._bot_token: str = self._get_bot_token()
        self._bot_server: str = self._get_bot_server()
        self._database_connection_parameters: dict[
            str, str
        ] = self._get_database_connection_parameters()
        self._s3_connection_parameters:dict[str, str] = self._get_s3_connection_parameters()
        self._onec_user: str = self._get_onec_user()
        self._onec_pass: str = self._get_onec_pass()
        self._onec_host: str = self._get_onec_host()
    
    def _get_bot_token(self) -> str:
        bot_token = getenv("BOT_TOKEN")
        if not bot_token:
            raise DotEnvVariableNotFound("BOT_TOKEN")
        return bot_token
    
    def _get_bot_server(self) -> str:
        bot_server = TelegramAPIServer.from_base('http://localhost:8081')
        if not bot_server:
            raise DotEnvVariableNotFound("bot_server")
        return bot_server

    def _get_database_connection_parameters(self) -> dict[str, str]:
        for parameter in [
            "DB_HOST",
            "DB_PORT",
            "DB_USER",
            "DB_USER_PASSWORD",
            "DB_NAME",
        ]:
            if not getenv(parameter):
                raise DotEnvVariableNotFound(parameter)

        return {
            "host": getenv("DB_HOST"),
            "port": getenv("DB_PORT"),
            "user": getenv("DB_USER"),
            "password": getenv("DB_USER_PASSWORD"),
            "database": getenv("DB_NAME"),
        }

    def _get_s3_connection_parameters(self) -> dict[str, str]:
        for parameter in [
            "S3_ACCESS_KEY",
            "S3_SECRET_KEY",
            "S3_BUCKET",
            "S3_ENDPOINT",
            "S3_WEB",
        ]:
            if not getenv(parameter):
                raise DotEnvVariableNotFound(parameter)

        return {
            "S3_ACCESS_KEY": getenv("S3_ACCESS_KEY"),
            "S3_SECRET_KEY": getenv("S3_SECRET_KEY"),
            "S3_BUCKET": getenv("S3_BUCKET"),
            "S3_ENDPOINT": getenv("S3_ENDPOINT"),
            "S3_WEB": getenv("S3_WEB"),
        }

    def _get_onec_user(self) -> str:
        onec_user = getenv("ONEC_USER")
        if not onec_user:
            raise DotEnvVariableNotFound("ONEC_USER")
        return onec_user
    
    def _get_onec_pass(self) -> str:
        onec_pass = getenv("ONEC_PASS")
        if not onec_pass:
            raise DotEnvVariableNotFound("ONEC_PASS")
        return onec_pass
    
    def _get_onec_host(self) -> str:
        onec_host = getenv("ONEC_HOST")
        if not onec_host:
            raise DotEnvVariableNotFound("ONEC_HOST")
        return onec_host
    
    @property
    def bot_token(self) -> str:
        return self._bot_token
    
    @property
    def bot_server(self) -> str:
        return self._bot_server

    @property
    def database_connection_parameters(self) -> dict[str, str]:
        return self._database_connection_parameters
    
    @property
    def s3_params(self) -> dict[str, str]:
        return self._s3_connection_parameters
    
    @property
    def onec_user(self) -> str:
        return self._onec_user
    
    @property
    def onec_pass(self) -> str:
        return self._onec_pass
    
    @property
    def onec_host(self) -> str:
        return self._onec_host
        