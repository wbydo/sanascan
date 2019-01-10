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

interface CursolProperty {
  activeColumn: number;
  activeRow: number;
}

export type CursolState = (
  {mode: "normal", direction: "column"} & CursolProperty
) | (
  {mode: "normal", direction: "row"} & CursolProperty
) | (
  {mode: "proposal", direction: "column"} & CursolProperty
);

export interface RootState {
  configWindow: {
    isActive: boolean;
    scanSpeed: number;
  };
  cursol: CursolState;
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

export { selectors } from "./selectors";
export { operations } from "./operations";
