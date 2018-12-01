import * as Actions from "./actions";
import middleware from "./middlewares";
import reducer from "./reducers";
import * as types from "./types";

export const timerActions = Actions;
export const timerMiddleware = middleware;
export const timerReducer = reducer;
export const timerActionTypes = types;
