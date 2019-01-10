import { createStore, applyMiddleware } from "redux";
import { combineReducers} from "redux";

import { composeWithDevTools } from "redux-devtools-extension";

import { reducer as configWindowReducer } from "./state/configWindow";
import { reducer as cursolReducer } from "./state/cursol";
import { reducer as developerModeReducer } from "./state/developerMode";
import { reducer as estimatorReducer } from "./state/estimator";
import { reducer as timerReducer } from "./state/timer";

import { middlewares as timerEventMiddlewares } from "./cross/timerEvent";
import { middlewares as httpMiddlewares } from "./cross/http";

export interface RootState {
  configWindow: {
    isActive: boolean;
    scanSpeed: number;
  };
  cursol: {
    activeColumn: number;
  };
  developerMode: boolean;
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
  ...httpMiddlewares,
  ...timerEventMiddlewares,
];

const enhancer = composeWithDevTools(
  applyMiddleware(...middlewares),
);

export const reducer = combineReducers({
  configWindow: configWindowReducer,
  cursol: cursolReducer,
  developerMode: developerModeReducer,
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

export { operations } from "./operations";
