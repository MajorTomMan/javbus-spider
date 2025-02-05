package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Actress;
import com.jav.server.entity.base.BigImage;
import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Director;
import com.jav.server.entity.base.Label;
import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.SampleImage;
import com.jav.server.entity.base.Series;
import com.jav.server.entity.base.Studio;

import lombok.Data;

@Data
public class PageVO {
    Movie movie;
    Director director;
    List<Actress> actresses;
    Studio studio;
    Series series;
    Label label;
    BigImage bigImage;
    List<Category> categories;
    List<SampleImage> sampleImages;
}
