import { createStore, applyMiddleware } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";

import middlewares from "./middlewares";
import reducer from "./reducers";

export interface RootState {
  cursol: {
    activeColumn: number;
  };
  window: {
    configure: {
      isActive: boolean;
    },
    timer: {
      isActive: boolean;
      scanSpeed: number;
    },
  };
}

const enhancer = composeWithDevTools(
  applyMiddleware(...middlewares),
);

const store = createStore(
  reducer,
  enhancer,
);

export default store;
