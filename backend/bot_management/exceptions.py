class BotManagementException(Exception):
    """Excepción base para el módulo de gestión del bot"""
    pass

class NLPModelNotTrainedError(BotManagementException):
    """Excepción lanzada cuando se intenta usar el modelo sin entrenar"""
    pass

class InvalidTrainingDataError(BotManagementException):
    """Excepción para datos de entrenamiento inválidos"""
    pass