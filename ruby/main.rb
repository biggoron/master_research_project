class Wavelet
  attr_accessor :wav_symbol

  # Main wavelets are implemented as Procs which generate the
  # wavelet function as a Proc, given some parameters
  MORLET = Proc.new do |dif, freq|
    Proc.new do |t|
      mod = Math::exp(-0.5*dif*(t**2))
      arg = freq*t
      Complex.polar(mod, arg)
    end
  end
  # Need to implement other wavelets
  # ...

  def initialize(sym, real, wav_symbol, wav_proc)
  #TODO The sym, real, wav_symbol should be optional
  #TODO if sym and real are not given, they should be computed
    @c_r = real    
    @wav_proc = wav_proc
    @wav_symbol = wav_symbol
    @wav_proc = wav_proc
  end

  def complex?
    if @c_r == :complex then true else false end
  end
  def real?
    if @c_r == :real then true else false end
  end
  def max_value
    #TODO
  end
  
  def sample (n0, m, v, b, limit)
    # Compute t bound
    # TODO: get a better dichotomic search for the bound
    bound = 0.5
    samples = []
    condition = false
    step = Integer(n0/2)
    until condition do
      condition = true
      lower_quartile = step - 2
      (lower_quartile .. step).each do |s|
        condition = false unless                                      \
                          @wav_proc.call(s*bound/step).abs < limit \
                          or                                          \
                          @wav_proc.call(-1*s*bound/step).abs < limit 
      end
      bound *= 1.05
    end
    a = 2**(m/v).to_f
    ta = 2*bound.to_f/(a*n0)
    sqrt_a = Math::sqrt(a)
    time_unit = 2*bound.to_f / n0
    
    sampled_wavelet = Proc.new do |t|
      t = t - b
      norm_t = t.to_f / a.to_f
      if norm_t.abs > n0/2 
        0
      else
        @wav_proc.call(norm_t*time_unit).real
      end
    end

    return sampled_wavelet

  end

end


# Test sampling
morlet_wav = Wavelet.new(true, :complex, :morlet,
Wavelet::MORLET.call(2, 0))
sample = morlet_wav.sample(20, 4, 1, 70, 0.01)
(-100 .. 100).each do |i|
  puts sample.call(i)
end


# Test MORLET bloc and compute 
#morlet_wav = WF::MORLET.call(2,0)
#(0..10).each do |t|
# norm = morlet_wav.call(t).abs 
# puts t if norm > 0.01
#end




#test morlet function
#morlet_wav = WaveletFactory::morlet(2, 0)
#(-10..10).each do |t|
# puts morlet_wav.call(t)
#end

