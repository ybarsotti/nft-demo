import pytest

from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, \
    get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('Only for local testing')

    advanced_collectible, creation_tx = deploy_and_create()
    requestId = creation_tx.events['requestedCollectible']['requestId']
    random_number = 777
    get_contract('vrf_coordinator').callBackWithRandomness(requestId,
                                                           random_number,
                                                           advanced_collectible.address,
                                                           {
                                                               "from": get_account()})
    # ASsert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
