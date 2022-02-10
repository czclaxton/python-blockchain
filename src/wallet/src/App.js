import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import TransactionList from "./components/TransactionList";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [id, setId] = useState("");
  const [chain, setChain] = useState([]);
  const [transactionList, setTransactionList] = useState([]);
  const [bal, setBal] = useState(0);
  const [trigger] = useState(false);

  const handleLogin = (evt) => {
    evt.preventDefault();
    setLoggedIn(!loggedIn);
  };

  const resetBalance = () => {
    setBal(0);
  };

  useEffect(() => {
    resetBalance();
    if (chain.length >= 2 && loggedIn === true) {
      const list = [].concat([...chain.map((item) => item.transactions)]);
      const user = [];
      list.forEach((item) => {
        if (item.sender === id || item.receiver.slice(0, -1) === id) {
          user.push(item);
        }
        if (item.sender === id)
          setBal((currentBalance) => {
            currentBalance += Number(item.amount);
          });
        if (item.receiver.slice(0, -1) === id)
          setBal((currentBalance) => {
            currentBalance += Number(item.amount);
          });
      });
      setTransactionList(user);
    }
  }, [loggedIn, chain, trigger, id]);

  useEffect(() => {
    if (loggedIn === true) {
      axios
        .get("http://localhost:5000/chain")
        .then((res) => {
          setChain(res.data.chain);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [loggedIn]);

  const handleChange = (evt) => {
    setId(evt.target.value);
  };

  return (
    <div className="App">
      <header>
        <h1>HEADER</h1>
        {loggedIn && (
          <div>
            <div onClick={trigger}>Click Here</div>
            <button onClick={handleLogin}>LOG OUT</button>
          </div>
        )}
      </header>
      <div>
        {loggedIn && (
          <div>
            <h1>{id}</h1>
            <h1>Wallet: {bal}</h1>
          </div>
        )}
        {loggedIn === false ? (
          <form onSubmit={handleLogin}>
            <input name="id" onChange={handleChange} value={id}></input>
            <button>LOG IN</button>
          </form>
        ) : (
          <div>
            {transactionList.length >= 1 &&
              transactionList.map((transaction) => {
                return <TransactionList transaction={transaction} />;
              })}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
