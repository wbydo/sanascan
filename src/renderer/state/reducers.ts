import { combineReducers } from "redux";

import {Action} from "./actions";
import * as types from "./types";

import { cursolReducer } from "./cursol/index";
import { timerReducer } from "./timer/index";

// /////////////////////////////////////////////
// windowReducer

interface WindowState {
  configure: {
    isActive: boolean;
  };
  timer: {
    isActive: boolean;
    scanSpeed: number;
  };
}

const windowReducer = (state: WindowState | undefined, action: Action): WindowState => {
  if (state === undefined) {
    return {
      configure: {
        isActive: false,
      },
      timer: timerReducer(state, action),
    };
  }

  if (action.type === types.ACTIVATE_CONFIGURE_WINDOW) {
    return {
      configure: {
        isActive: true,
      },
      timer: {
        isActive: false,
        scanSpeed: state.timer.scanSpeed,
      },
    };
  }

  return {
    configure: {
      isActive: state.configure.isActive,
    },
    timer: timerReducer(state.timer, action),
  };
};
// windowReducer
// /////////////////////////////////////////////

// /////////////////////////////////////////////
// root

const reducer = combineReducers({
  cursol: cursolReducer,
  window: windowReducer,
});

export default reducer;

// root
// /////////////////////////////////////////////
