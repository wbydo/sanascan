import { createStore, applyMiddleware } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";

import middlewares from "./middlewares";
import reducer from "./reducers";

const enhancer = composeWithDevTools(
  applyMiddleware(...middlewares),
);

const store = createStore(
  reducer,
  enhancer,
);

export default store;
