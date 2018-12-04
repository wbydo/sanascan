import { combineReducers } from "redux";

import { configWindowReducer } from "./configWindow/index";
import { cursolReducer } from "./cursol/index";
import { timerReducer } from "./timer/index";
import { estimatorReducer } from "./estimator";

export interface RootState {
  configWindow: {
    isActive: boolean;
    scanSpeed: number;
  };
  cursol: {
    activeColumn: number;
  };
  timer: {
    isActive: boolean;
    scanSpeed: number;
  };
  estimator: {
    id: number | null;
  };
}

const reducer = combineReducers({
  configWindow: configWindowReducer,
  cursol: cursolReducer,
  estimator: estimatorReducer,
  timer: timerReducer,
});

export default reducer;
