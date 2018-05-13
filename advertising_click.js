var presses = 0;
NRF.setAdvertising(
  {}
  ,{manufacturer: 0x0590, manufacturerData:[presses], interval:1000}
);

setWatch(function() {
  presses++;
  NRF.setAdvertising(
    {},
    {manufacturer: 0x0590, manufacturerData:[presses], interval:1000}
  );
}, BTN, {edge:"rising", repeat:1, debounce:20});
