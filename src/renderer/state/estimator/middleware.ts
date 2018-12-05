import { Dispatch } from "redux";
import { URL } from "url";
import { stringify } from "querystring";

import { RootState } from "../reducers";

import * as types from "./types";
import * as actions from "./actions";

import { url as baseUrl } from "../../constant";

import SanascanError from "../../error";

import { setTimeoutPromise } from "../../myutil";

import { timerActions } from "../timer";

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: actions.Action) => void;

const TRY_NUMBER = 10;
const TIMEOUT = 5000;

const tryFethIdOnce = async (storeDispatch: Dispatch) => {
  const response = await fetch(baseUrl, {method: "POST"});
  const result = await response.json();

  if (result.eid !== undefined && (typeof result.eid === "number")) {
    storeDispatch(actions.fetchId("done"));
    storeDispatch(actions.setId(result.eid as number));
    return;
  } else {
    throw new SanascanError();
  }
};

const fetchIdStart = async (storeDispatch: Dispatch) => {
  let isSuccess = false;
  for (const _ of Array(TRY_NUMBER).keys()) {
    if (isSuccess) {
      break;
    }
    try {
      await tryFethIdOnce(storeDispatch).then(() => { isSuccess = true; });
    } catch (err) {
      await setTimeoutPromise(TIMEOUT);
    }
  }

  if (isSuccess) {
    storeDispatch(actions.fetchId("done"));
  } else {
    storeDispatch(actions.fetchId("error"));
  }
};

const processFetchIdAction = (next: Dispatch, storeDispatch: Dispatch, action: actions.Action) => {
  switch (action.payload.status) {
    case "start":
      next(action);
      fetchIdStart(storeDispatch);
      break;

    case "done":
      next(action);
      storeDispatch(timerActions.start());
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
      processFetchIdAction(next, store.dispatch, action);
      break;

    case types.SEND_KEY:
      next(action);
      const id = store.getState().estimator.id;
      if (id === null) {
        throw new SanascanError();
      }

      if (action.payload.key === undefined) {
        throw new SanascanError();
      }

      const url = new URL(id.toString(), baseUrl);
      const query = stringify({key: action.payload.key.toString()});
      fetch(url.toString(), {
        body: query.toString(),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "POST",
      }).then((resp) => {
        return Promise.resolve(resp.json());
      }).then((json) => {
        if (json.result === undefined) {
          throw new SanascanError();
        }
        next(actions.setResult(json.result));
      });

    default:
      next(action);
  }
};

export default middleware;
