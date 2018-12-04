import { Dispatch } from "redux";

import { RootState } from "../reducers";

import * as types from "./types";
import * as actions from "./actions";

import * as timerActions from "../timer";

import { url } from "../../constant";

import SanascanError from "../../error";

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: actions.Action) => void;

const tryFethIdOnce = async (next: Dispatch) => {
  console.log(new Date());
  return await fetch(url, {method: "POST"})
    .then((resp) => resp.json())
    .then((result) => {
      if (result.eid !== undefined && (typeof result.eid === "number")) {
        console.log(result);
        return next(actions.setID(result.eid as number));
      } else {
        throw new SanascanError();
      }
    });
};

const processFetchIDAction = async (
    next: Dispatch,
    action: actions.Action,
    ) => {

  switch (action.payload.status) {
    case "start":
      next(action);

      let isSuccess = false;
      for (const _ of Array(5).keys()) {
        if (isSuccess) {
          console.log(isSuccess);
          break;
        }
        console.log(_);
        try {
          await tryFethIdOnce(next).then(() => { isSuccess = true; });
        } catch (err) {
          console.log(err);
          await new Promise((resolve, _) => {
            setTimeout(() => {
              console.log("error");
              resolve();
            }, 1000);
          });
        }
      }

      break;
  }
};

const middleware: Middleware
    = (store: Store) => (next: Dispatch) => (action: actions.Action) => {

  switch (action.type) {
    case types.FETCH_ID:
      if (action.payload.status === undefined) {
        throw new SanascanError();
      }
      processFetchIDAction(next, action);
      break;

    default:
      next(action);
  }
};

export default middleware;
