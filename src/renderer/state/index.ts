import { createStore, applyMiddleware } from "redux";
import { combineReducers } from "redux";

import { composeWithDevTools } from "redux-devtools-extension";

import { configWindowReducer } from "./configWindow";

import { cursolReducer } from "./cursol";

import { estimatorReducer } from "./estimator";
import { estimatorMiddleware } from "./estimator";

import { timerMiddleware } from "./timer";
import { timerReducer } from "./timer";

export interface RootState {
  configWindow: {
    isActive: boolean;
    scanSpeed: number;
  };
  cursol: {
    activeColumn: number;
  };
  timer: {
    id: number | null;
    isActive: boolean;
    scanSpeed: number;
  };
  estimator: {
    id: number | null;
    result: string;
  };
}

const middlewares = [
  timerMiddleware,
  estimatorMiddleware,
];

const enhancer = composeWithDevTools(
  applyMiddleware(...middlewares),
);

export const reducer = combineReducers({
  configWindow: configWindowReducer,
  cursol: cursolReducer,
  estimator: estimatorReducer,
  timer: timerReducer,
});

export const store = createStore(
  reducer,
  enhancer,
);
