import { Dispatch } from "redux";

import { middleware as fetchIdMiddleware } from "./fetchId";
import { middleware as sendKeyMiddleware } from "./sendKey";
import { middleware as resetMiddleware } from "./reset";

import { RootState } from "../../..";

export interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

export const middlewares = [
  fetchIdMiddleware,
  sendKeyMiddleware,
  resetMiddleware,
];
