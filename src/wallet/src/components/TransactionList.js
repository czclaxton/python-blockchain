import React from "react";

const TransactionList = ({ transaction }) => {
  return (
    <div>
      <p>Sender: {transaction.sender}</p>
      <p>Receiver: {transaction.receiver}</p>
      <p>Amount: {transaction.amount}</p>
    </div>
  );
};

export default TransactionList;
