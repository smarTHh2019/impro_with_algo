#########################
# impro_with_algo       #
#########################
# author: Thomas Heller #
#########################

use_bpm 120
chord_list = [chord(:C4, "7"),chord(:C4, "7"),chord(:C4, "7"),chord(:C4, "7"),]

# dummy data for received phrase
midi_pitch = ring 62, 62
midi_rhytm = ring 8, 8

define :func_play_impro do |melo_ring, rhym_ring|
  cue :start_play_impro
  tick_reset
  print melo_ring
  print rhym_ring
  melo_ring.to_a.length.times do
    tick
    play  melo_ring.look
    sleep rhym_ring.look
  end
end

live_loop :play_background_beat do
  sample :drum_heavy_kick, amp: 0.25
  sleep 1
end

live_loop :play_background_chords do
  cue :start_of_phrase
  chord_list.each do |x|
    play x, release: 3.5
    sleep 4
  end
end

live_loop :request_python_improvisation do
  sync :start_of_phrase
  use_osc "localhost", 4545
  osc "/impro/phrase", 4     # request 4 bars of improvisation
  sync :start_play_impro     # wait until the impro is playing before requesting a new one
end

live_loop :receive_improvisation do
  use_real_time
  melo_received = sync "/osc:127.0.0.1:*/*_melo"
  rhym_received = sync "/osc:127.0.0.1:*/*_rhym"
  set :midi_pitch, melo_received
  set :midi_rhytm, rhym_received
  cue :phrase_ready
end

live_loop :play_received_improvisation do
  use_synth :prophet      # => set Sonic Pi to an instrument you like
  sync :phrase_ready      # an impro was received
  sync :start_of_phrase   # a phrase starts now
  ml=get(:midi_pitch)
  rh=get(:midi_rhytm)
  ml=ml.ring
  rh=rh.ring
  func_play_impro ml, rh
end
