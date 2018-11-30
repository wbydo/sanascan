import * as React from "react";
import * as ReactDOM from "react-dom";
import { createStore, applyMiddleware } from "redux";
import { Provider } from "react-redux";
import { composeWithDevTools } from "redux-devtools-extension";

import App from "./views/App";
import { rootReducer } from "./state/reducers";
import { middleware } from "./state/middleware";

const enhancer = composeWithDevTools(
  applyMiddleware(middleware),
);

const store = createStore(
  rootReducer,
  enhancer,
);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root"),
);
