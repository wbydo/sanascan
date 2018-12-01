import * as React from "react";
import * as ReactDOM from "react-dom";
import { Provider } from "react-redux";

import App from "./views/App";
import store from "./state/index";

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root"),
);
