from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import AMP
import pickle
from twisted.internet.defer import inlineCallbacks, returnValue
from onlineballotregulator.network_commands import *

from crochet import setup, run_in_reactor
setup()

@run_in_reactor
@inlineCallbacks
def searchUser(user_id):
    """
    http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

    Blocking call to the ballot server to request the ballots for a particular user.

    :return: EventualResult
    """

    # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
    destination_deferred = yield TCP4ClientEndpoint(reactor, '127.0.0.1', 5434)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineBallotRegulator_SearchBallotRegisterForUserId, user_id=user_id)

    def format_results(pickled_result):

        # First unpickle the results.
        result = pickle.loads(pickled_result['ok'])

        # Transform the list results into a dictionary.
        record_list = []
        for record in result:
            mapper = {}
            mapper['user_id'] = record[0]
            mapper['ballot_id'] = record[1]
            mapper['timestamp'] = record[2]
            mapper['ballot_name'] = record[3]
            mapper['ballot_address'] = record[4]
            # Append each row's dictionary to a list
            record_list.append(mapper)

        return record_list

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))


@run_in_reactor
@inlineCallbacks
def getAllBallots():
    """
    http://crochet.readthedocs.io/en/latest/api.html#run-in-reactor-asynchronous-results

    Blocking call to the ballot server to request the ballots for a particular user.

    :return: EventualResult
    """

    # NOTE: using inline callbacks here so we dont have to write/wait for callbacks.
    destination_deferred = yield TCP4ClientEndpoint(reactor, '127.0.0.1', 5434)
    connection_deferred = yield connectProtocol(destination_deferred, AMP())
    result_deferred = yield connection_deferred.callRemote(OnlineBallotRegulator_SearchBallotsAvailableForAllBallots)

    def format_results(pickled_result):

        # First unpickle the results.
        result = pickle.loads(pickled_result['ok'])

        # Transform the list results into a dictionary.
        record_list = []
        for record in result:
            mapper = {}
            mapper['ballot_id'] = record[0]
            mapper['ballot_name'] = record[1]
            mapper['ballot_address'] = record[2]
            mapper['timestamp'] = record[3]
            # Append each row's dictionary to a list
            record_list.append(mapper)

        return record_list

    # Inlinecallback return value.
    returnValue(format_results(result_deferred))

if __name__ == '__main__':
    # test = searchUser(1234).wait(5)
    test = getAllBallots().wait(5)
    print(test)

