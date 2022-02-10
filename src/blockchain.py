import hashlib
import json
from time import time
from uuid import uuid4
from random import randint

from flask import Flask, jsonify, request
from flask_cors import CORS


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True).encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(string_object)

        hex_hash = raw_hash.hexdigest()

        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
        # return True or False

    def new_transaction(self, sender, receiver, amount):
        """
        creates a new transaction to go into the next mined block
        :param transaction_id: <int> transaction id
        :param sender: <str> sender's name
        :param receiver: <str> receiver's name
        :param amount: <float> amount of transaction
        :return: <index> the index of the block that will hold the transactions
        """

        self.current_transactions.append({
            'transaction_id': transaction_id,
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        return self.last_block['index'] + 1



app = Flask(__name__)
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/update_user', methods=['POST'])
def update_user():

    data = request.get_json()

    # required = ['user']
    # if not all(k in data for k in required):
    #     response = {'message': 'missing values'}
    #     return jsonify(response), 400

    User().update_user(data["user"])

    # user = User().get_user()

    response = {
        'message': 'success'
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()

    required = ['sender', 'receiver', 'amount']
    if not all(k in data for k in required):
        response = {'message': 'missing values'}
        return jsonify(response), 400

    # create new transaction
    index = blockchain.new_transaction(
        data['sender'], data['receiver'], data['amount'])

    response = {
        'message': f'Transaction will post block {index}.'
    }
    return jsonify(response), 201


@app.route('/mine', methods=['POST'])
def mine():

    data = request.get_json()
    required = ['proof', 'id']
    if not all(k in data for k in required):
        response = {'message': 'missing values'}
        return jsonify(response), 400

    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True)

    if blockchain.valid_proof(last_block_string, data['proof']):
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(data['proof'], previous_hash)

        blockchain.new_transaction(
            sender="0", receiver=data['id'], amount=100)

        response = {
            'message': 'new block forged'
        }
        return jsonify(response), 200

    else:

        response = {
            'message': 'proof is invalid or already submitted'
        }
        return jsonify(response), 401
    


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def get_last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


@app.route('/user', methods=['GET'])
def get_user():

    user = User().get_user()
    transactions_list = User().get_transactions()
    balance = User().get_balance()

    response = {
        'user': user,
        'transactions_list': transactions_list,
        'balance': balance
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)