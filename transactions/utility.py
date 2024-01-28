from . import models


def create_transaction_log(transaction_instance: models.Transaction, error: dict):
    '''
    create transaction log

    format :
        {
            'history': {
                logs: [
                    {
                        'status': <str>,
                        'error': <str>,
                        'timestamp': <date-time>
                    },
                ]
            }
        }
    '''
    
    _history = transaction_instance.metadata.get('history', {})
    _logs = _history.get('logs', [])
    _logs.append(error)

    txn_metadata = {
        'history': {
            'logs': _logs
        }
    }

    transaction_instance.metadata = txn_metadata
    transaction_instance.save()