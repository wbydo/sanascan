import { combineReducers } from "redux";

import { configWindowReducer } from "./configWindow/index";
import { cursolReducer } from "./cursol/index";
import { timerReducer } from "./timer/index";

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
}

const reducer = combineReducers({
  configWindow: configWindowReducer,
  cursol: cursolReducer,
  timer: timerReducer,
});

export default reducer;
