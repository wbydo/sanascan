import snapshotDiff from "snapshot-diff";

import { reducer } from "sanascan/renderer/redux";

import { actions } from "sanascan/renderer/redux/state/cursol";

import { MAX_COLUMN_INDEX, MAX_ROW_INDEX } from "sanascan/renderer/constant";

import { initialState } from "./initialState";

describe("modeが設定出来る", () => {
  for (const i of ["normal", "proposal"]) {
    test(i + "の場合", () => {
      const arg = i as "normal" | "proposal";

      const result = reducer(
        initialState,
        actions.setMode(arg),
      );

      expect(
        snapshotDiff( initialState, result),
      ).toMatchSnapshot();
    });
  }
});

describe("directionが設定出来る", () => {
  for (const d of ["column", "row"]) {
    for (const m of ["normal", "proposal"]) {
      test("mode:" + m + " direction: " + d, () => {
        const target = reducer(
          initialState,
          actions.setMode(m as "normal" | "proposal"),
        );

        const result = reducer(
          target,
          actions.setDirection(d as "column" | "row"),
        );

        expect(
          snapshotDiff(target, result),
        ).toMatchSnapshot();
      });
    }
  }
});

describe("increment", () => {
  const params = [{
      change: {activeRow: MAX_ROW_INDEX},
      direction: "row" as "column" | "row",
      mode: "normal" as "normal" | "proposal",
    }, {
      change: {activeColumn: MAX_COLUMN_INDEX},
      direction: "column" as "column" | "row",
      mode: "normal" as "normal" | "proposal",
    }, {
      change: {activeColumn: MAX_COLUMN_INDEX},
      direction: "column" as "column" | "row",
      mode: "proposal" as "normal" | "proposal",
    },
  ];

  for (const p of params) {
    describe("mode:" + p.mode + " direction: " + p.direction, () => {
      test("1増える", () => {
        const setMode = reducer(
          initialState,
          actions.setMode(p.mode),
        );

        const target = reducer(
          setMode,
          actions.setDirection(p.direction),
        );

        const result = reducer(
          target,
          actions.increment(),
        );

        expect(
          snapshotDiff(target, result),
        ).toMatchSnapshot();
      });

      test("0に戻る", () => {
        const setMode = reducer(
          initialState,
          actions.setMode(p.mode),
        );

        const setDirection = reducer(
          setMode,
          actions.setDirection(p.direction),
        );

        const change = p.change;

        const target = {
          ...setDirection,
          cursol: {
            ...setDirection.cursol,
            ...change,
          },
        };

        const result = reducer(
          target,
          actions.increment(),
        );

        expect(
          snapshotDiff(target, result),
        ).toMatchSnapshot();
      });

    });
  }
});

describe("RESET", () => {
  const params = [{
      change: {activeRow: MAX_ROW_INDEX},
      direction: "row" as "column" | "row",
      mode: "normal" as "normal" | "proposal",
    }, {
      change: {activeColumn: MAX_COLUMN_INDEX},
      direction: "column" as "column" | "row",
      mode: "normal" as "normal" | "proposal",
    }, {
      change: {activeColumn: MAX_COLUMN_INDEX},
      direction: "column" as "column" | "row",
      mode: "proposal" as "normal" | "proposal",
    },
  ];

  for (const p of params) {
    describe("mode:" + p.mode + " direction: " + p.direction, () => {
      test("0に戻る", () => {

        const target = reducer(
          {
            ...initialState,
            cursol: {
              ...initialState.cursol,
              activeColumn: 4,
              activeRow: 3,
            },
          },
          actions.setDirection(p.direction),
        );

        const result = reducer(
          target,
          actions.reset(),
        );

        expect(
          snapshotDiff(target, result),
        ).toMatchSnapshot();
      });
    });
  }
});
