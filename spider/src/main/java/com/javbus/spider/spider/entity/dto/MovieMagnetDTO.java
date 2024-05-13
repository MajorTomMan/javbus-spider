package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Magnet;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;

@Data
public class MovieMagnetDTO {
    private Movie movie;
    private List<Magnet> magnets;
}
