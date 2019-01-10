import { createStore, applyMiddleware } from "redux";
import { combineReducers} from "redux";

import { composeWithDevTools } from "redux-devtools-extension";

import { middleware } from "./middleware";

import { reducer as configWindowReducer } from "./configWindow";
import { reducer as cursolReducer } from "./cursol";
import { reducer as estimatorReducer } from "./estimator";
import { reducer as timerReducer } from "./timer";
import { middleware as timerMiddleware } from "./timer";

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
  middleware,
  timerMiddleware,
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

export const selectors = (state: RootState) => {
  return {
    activeColumn: state.cursol.activeColumn,
    configureWindowIsActive: state.configWindow.isActive,
    configureWindowScanSpeed: state.configWindow.scanSpeed,
    result: state.estimator.result,
    timerScanSpeed: state.timer.scanSpeed,
  };
};

import { forViews } from "./operations";
export const operations = { forViews };
